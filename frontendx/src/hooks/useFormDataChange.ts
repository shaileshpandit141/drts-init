import { useState, ChangeEvent } from "react";

type FormData = {
  [key: string]: any;
};

export function useFormDataChange<T extends FormData>(initialFormData: T) {
  if (typeof initialFormData !== "object" || initialFormData === null) {
    throw new Error(
      "The useFormHook only accepts the initialData value as an object.",
    );
  }

  const [formData, setFormData] = useState<T>(initialFormData);

  function handleFormDataChange(
    event: ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >,
  ) {
    const { name, type, value } = event.target;

    // Narrow down to HTMLInputElement for 'checked'
    const checked =
      type === "checkbox" && event.target instanceof HTMLInputElement
        ? event.target.checked
        : undefined;

    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: type === "checkbox" ? checked : value,
    }));
  }

  return [formData, handleFormDataChange] as const;
}
