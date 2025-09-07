import { useState, useCallback, useMemo } from "react";

type SyncValidator<T> = (values: T) => Partial<Record<keyof T, string>>;
type FieldValidator<T> = (
  value: any,
  values: T
) => string | undefined | Promise<string | undefined>;

interface UseSmartFormOptions<T> {
  initialValues: T;
  onSubmit: (values: T) => void | Promise<void>;
  validate?: SyncValidator<T>;
  fieldValidators?: Partial<Record<keyof T, FieldValidator<T>>>;
}

export function useSmartForm<T extends Record<string, any>>({
  initialValues,
  onSubmit,
  validate,
  fieldValidators = {},
}: UseSmartFormOptions<T>) {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});
  const [touched, setTouched] = useState<Partial<Record<keyof T, boolean>>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [step, setStep] = useState(0);
  const [disableValidation, setDisableValidation] = useState(false);
  const [validateOnChange, setValidateOnChange] = useState(false);

  // --- Value parsers ---
  const valueParsers = useMemo<
    Record<string, (e: React.ChangeEvent<any>) => any>
  >(
    () => ({
      checkbox: (e) => e.target.checked,

      file: (e) => {
        const { files, multiple } = e.target;
        return multiple ? files : files?.[0];
      },

      number: (e) =>
        e.target.value === "" ? undefined : Number(e.target.value),

      range: (e) =>
        e.target.value === "" ? undefined : Number(e.target.value),

      date: (e) =>
        e.target.value === "" ? undefined : new Date(e.target.value),

      "datetime-local": (e) =>
        e.target.value === "" ? undefined : new Date(e.target.value),

      selectMultiple: (e) =>
        Array.from(e.target.options)
          .filter((o: any) => o.selected)
          .map((o: any) => o.value),
    }),
    []
  );

  // Default parser: returns trimmed string
  const defaultParser = (e: React.ChangeEvent<any>) =>
    typeof e.target.value === "string" ? e.target.value.trim() : e.target.value;

  const normalizeValue = useCallback(
    (e: React.ChangeEvent<any>) => {
      const { type, tagName, multiple } = e.target;

      if (tagName === "SELECT" && multiple) {
        return valueParsers["selectMultiple"](e);
      }

      const parser = valueParsers[type];
      return parser ? parser(e) : defaultParser(e);
    },
    [valueParsers]
  );

  // --- Form-level validation ---
  const validateForm = useCallback(async (): Promise<
    Partial<Record<keyof T, string>>
  > => {
    let fieldErrors: Partial<Record<keyof T, string>> = {};

    if (validate) {
      fieldErrors = { ...fieldErrors, ...validate(values) };
    }

    for (const key in fieldValidators) {
      const validator = fieldValidators[key as keyof T];
      const val = values[key as keyof T];
      if (validator) {
        const result = await validator(val, values);
        if (result) fieldErrors[key as keyof T] = result;
      }
    }

    Object.keys(fieldErrors).forEach((key) => {
      if (!fieldErrors[key as keyof T]) {
        delete fieldErrors[key as keyof T];
      }
    });

    setErrors(fieldErrors);
    return fieldErrors;
  }, [fieldValidators, validate, values]);

  const validateStep = async (fields: (keyof T)[]) => {
    const currentErrors: Partial<Record<keyof T, string>> = {};

    for (const field of fields) {
      const val = values[field];
      let customError: string | undefined;

      const validator = fieldValidators[field];
      if (validator) {
        customError = await validator(val, values);
      }

      if (customError) {
        currentErrors[field] = customError;
      }
    }

    setErrors((prev) => ({ ...prev, ...currentErrors }));
    return currentErrors;
  };

  // --- Handlers ---
  const handleChange = useCallback(
    async (e: React.ChangeEvent<any>) => {
      const { name } = e.target;
      const newValue = normalizeValue(e);

      setValues((prev) => {
        const updated = { ...prev, [name]: newValue };

        if (validateOnChange && !disableValidation) {
          const key = name as keyof T;
          const val = updated[key];

          (async () => {
            setTouched((prev) => ({ ...prev, [key]: true }));

            let customError: string | undefined;
            const validator = fieldValidators[key];
            if (validator) {
              customError = await validator(val, updated);
            }

            setErrors((prev) => {
              const updatedErrors = { ...prev };
              if (customError) {
                updatedErrors[key] = customError;
              } else {
                delete updatedErrors[key];
              }
              return updatedErrors;
            });
          })();
        }

        return updated;
      });
    },
    [normalizeValue, validateOnChange, disableValidation, fieldValidators]
  );

  const handleBlur = useCallback(
    async (e: React.FocusEvent<any>) => {
      if (disableValidation) return;

      const { name } = e.target;
      const key = name as keyof T;
      const val = values[key];

      setTouched((prev) => ({ ...prev, [key]: true }));

      let customError: string | undefined;
      const validator = fieldValidators[key];
      if (validator) {
        customError = await validator(val, values);
      }

      setErrors((prev) => {
        const updated = { ...prev };
        if (customError) {
          updated[key] = customError;
        } else {
          delete updated[key];
        }
        return updated;
      });
    },
    [disableValidation, values, fieldValidators]
  );

  const handleSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();
      setIsSubmitting(true);

      const fieldErrors = await validateForm();
      const hasErrors = Object.keys(fieldErrors).length > 0;

      if (!hasErrors) {
        await onSubmit(values);
      }

      setIsSubmitting(false);
    },
    [validateForm, onSubmit, values]
  );

  // --- Utils ---
  const register = (name: keyof T) => {
    const value = values[name] as any;
    const props: any = {
      name,
      onChange: handleChange,
      onBlur: handleBlur,
    };

    if (typeof value === "boolean") {
      props.checked = value;
    } else if (value instanceof File || value instanceof FileList) {
      // no binding for file inputs
    } else if (Array.isArray(value)) {
      props.value = value;
    } else {
      props.value = value ?? "";
    }

    return props;
  };

  const showError = (name: keyof T) => {
    return Boolean(touched[name] && errors[name]);
  };

  const isValid = useMemo(() => {
    return Object.values(errors).every((error) => !error);
  }, [errors]);

  const nextStep = async (stepFields?: (keyof T)[]) => {
    if (!stepFields) return setStep((s) => s + 1);

    const stepErrors = await validateStep(stepFields);
    const hasErrors = Object.keys(stepErrors).length > 0;
    if (!hasErrors) setStep((s) => s + 1);
  };

  const prevStep = () => setStep((s) => s - 1);

  const reset = () => {
    setDisableValidation(true);

    setValues(initialValues);
    setErrors({});
    setTouched({});
    setIsSubmitting(false);

    setTimeout(() => setDisableValidation(false), 0);
  };

  return {
    values,
    errors,
    touched,
    isSubmitting,
    isValid,
    step,
    register,
    handleChange,
    handleBlur,
    handleSubmit,
    setValues,
    setErrors,
    showError,
    setDisableValidation,
    setValidateOnChange,
    reset,
    nextStep,
    prevStep,
    setStep,
  };
}
