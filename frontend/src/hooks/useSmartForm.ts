import { useState, useMemo } from "react";

type SyncValidator<T> = (values: T) => Partial<Record<keyof T, string>>;
type FieldValidator<T> = (
  value: any,
  values: T
) => string | undefined | Promise<string | undefined>;

interface UseSmartFormOptions<T> {
  initialValues: T;
  validateOnChange?: boolean;
  validateOnBlur?: boolean;
  fieldValidators?: Partial<Record<keyof T, FieldValidator<T>>>;
  validate?: SyncValidator<T>;
  onSubmit: (values: T) => void | Promise<void>;
}

interface UseSmartFormReturn<T> {
  values: T;
  errors: Partial<Record<keyof T, string>>;
  touched: Partial<Record<keyof T, boolean>>;
  isSubmitting: boolean;
  isValid: boolean;
  step: number;

  register: (name: keyof T) => any;
  handleSubmit: (e: React.FormEvent) => Promise<void>;
  hasError: (name: keyof T) => boolean;

  nextStep: (fields?: (keyof T)[]) => Promise<void>;
  prevStep: () => void;
  reset: () => void;
}

// --- Type guards for File and FileList ---
function isFile(val: unknown): val is File {
  return typeof File !== "undefined" && val instanceof File;
}

function isFileList(val: unknown): val is FileList {
  return typeof FileList !== "undefined" && val instanceof FileList;
}

export function useSmartForm<T extends Record<string, any>>({
  initialValues,
  validateOnChange = false,
  validateOnBlur = true,
  fieldValidators = {},
  validate,
  onSubmit,
}: UseSmartFormOptions<T>): UseSmartFormReturn<T> {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});
  const [touched, setTouched] = useState<Partial<Record<keyof T, boolean>>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [step, setStep] = useState(0);

  // --- Value Parsing ---
  const valueParsers = {
    checkbox: (e: React.ChangeEvent<HTMLInputElement>) => e.target.checked,
    file: (e: React.ChangeEvent<HTMLInputElement>) =>
      e.target.multiple ? e.target.files : e.target.files?.[0],
    number: (e: React.ChangeEvent<HTMLInputElement>) =>
      e.target.value === "" ? undefined : Number(e.target.value),
    range: (e: React.ChangeEvent<HTMLInputElement>) =>
      e.target.value === "" ? undefined : Number(e.target.value),
    date: (e: React.ChangeEvent<HTMLInputElement>) =>
      e.target.value === "" ? undefined : new Date(e.target.value),
    "datetime-local": (e: React.ChangeEvent<HTMLInputElement>) =>
      e.target.value === "" ? undefined : new Date(e.target.value),
    selectMultiple: (e: React.ChangeEvent<HTMLSelectElement>) =>
      Array.from(e.target.selectedOptions).map((o) => o.value),
  };

  const defaultParser = (e: React.ChangeEvent<any>) =>
    typeof e.target.value === "string" ? e.target.value.trim() : e.target.value;

  const normalizeValue = (e: React.ChangeEvent<any>) => {
    const { type, tagName, multiple } = e.target;
    if (tagName === "SELECT" && multiple) return valueParsers.selectMultiple(e);
    return (
      valueParsers[type as keyof typeof valueParsers]?.(e) ?? defaultParser(e)
    );
  };

  // --- Validation helpers ---
  const runValidator = async (key: keyof T, value: any, allValues: T) => {
    const fieldError = await fieldValidators[key]?.(value, allValues);

    const formErrors: Partial<Record<keyof T, string>> = validate
      ? validate(allValues)
      : {};

    return fieldError || formErrors[key];
  };

  const validateForm = async () => {
    const formErrors: Partial<Record<keyof T, string>> = validate
      ? { ...validate(values) }
      : {};

    for (const key in fieldValidators) {
      const err = await runValidator(key as keyof T, values[key], values);
      if (err) formErrors[key as keyof T] = err;
    }

    setErrors(formErrors);
    return formErrors;
  };

  const validateFields = async (fields: (keyof T)[]) => {
    const fieldErrors: Partial<Record<keyof T, string>> = {};

    for (const key of fields) {
      const err = await runValidator(key, values[key], values);
      if (err) fieldErrors[key] = err;
    }

    setErrors((prev) => ({ ...prev, ...fieldErrors }));
    return fieldErrors;
  };

  // --- Handlers ---
  const handleChange = (e: React.ChangeEvent<any>) => {
    const { name } = e.target;
    const key = name as keyof T;
    const newValue = normalizeValue(e);

    setValues((prev) => {
      const updated = { ...prev, [key]: newValue };

      if (validateOnChange) {
        setTouched((t) => ({ ...t, [key]: true }));
        runValidator(key, newValue, updated).then((err) =>
          setErrors((prevErr) => {
            const updatedErrors = { ...prevErr };
            if (err) updatedErrors[key] = err;
            else delete updatedErrors[key];
            return updatedErrors;
          })
        );
      }

      return updated;
    });
  };

  const handleBlur = (e: React.FocusEvent<any>) => {
    if (!validateOnBlur) return;
    const key = e.target.name as keyof T;
    const value = values[key];
    setTouched((t) => ({ ...t, [key]: true }));

    runValidator(key, value, values).then((err) =>
      setErrors((prev) => {
        const updated = { ...prev };
        if (err) updated[key] = err;
        else delete updated[key];
        return updated;
      })
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    const formErrors = await validateForm();
    if (Object.keys(formErrors).length === 0) {
      await onSubmit(values);
    }
    setIsSubmitting(false);
  };

  // --- Utils ---
  const register = (name: keyof T) => {
    const value = values[name];
    return {
      name,
      onChange: handleChange,
      onBlur: handleBlur,
      ...(typeof value === "boolean"
        ? { checked: value }
        : isFile(value) || isFileList(value)
        ? {}
        : { value: value ?? "" }),
    };
  };

  const hasError = (name: keyof T) => Boolean(touched[name] && errors[name]);

  const isValid = useMemo(
    () => Object.values(errors).every((e) => !e),
    [errors]
  );

  const nextStep = async (fields?: (keyof T)[]) => {
    if (!fields) return setStep((s) => s + 1);
    const stepErrors = await validateFields(fields);
    if (Object.keys(stepErrors).length === 0) setStep((s) => s + 1);
  };

  const prevStep = () => setStep((s) => s - 1);

  const reset = () => {
    setValues(initialValues);
    setErrors({});
    setTouched({});
    setIsSubmitting(false);
    setStep(0);
  };

  return {
    values,
    errors,
    touched,
    isSubmitting,
    isValid,
    step,
    register,
    handleSubmit,
    hasError,
    nextStep,
    prevStep,
    reset,
  };
}
