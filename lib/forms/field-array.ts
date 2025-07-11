import { useFieldArray, UseFieldArrayReturn, Control } from 'react-hook-form';

interface UseFormFieldArrayOptions<T extends Record<string, any>> {
  control: Control<T>;
  name: string;
}

export function useFormFieldArray<T extends Record<string, any>>(
  options: UseFormFieldArrayOptions<T>
): UseFieldArrayReturn<T> & {
  moveUp: (index: number) => void;
  moveDown: (index: number) => void;
  duplicate: (index: number) => void;
} {
  const fieldArray = useFieldArray({
    control: options.control,
    name: options.name as any,
  });
  
  const moveUp = (index: number) => {
    if (index > 0) {
      fieldArray.swap(index, index - 1);
    }
  };
  
  const moveDown = (index: number) => {
    if (index < fieldArray.fields.length - 1) {
      fieldArray.swap(index, index + 1);
    }
  };
  
  const duplicate = (index: number) => {
    const item = fieldArray.fields[index];
    fieldArray.insert(index + 1, { ...item, id: undefined } as any);
  };
  
  return { 
    ...fieldArray, 
    moveUp, 
    moveDown,
    duplicate,
  };
}

// Common form validation patterns
export const validationPatterns = {
  email: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
  phone: /^\+?[1-9]\d{1,14}$/,
  url: /^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$/,
  slug: /^[a-z0-9]+(?:-[a-z0-9]+)*$/,
  alphanumeric: /^[a-zA-Z0-9]+$/,
  numeric: /^\d+$/,
};

// Form field error helper
export function getFieldError(
  errors: Record<string, any>,
  name: string
): string | undefined {
  const keys = name.split('.');
  let error = errors;
  
  for (const key of keys) {
    if (!error[key]) return undefined;
    error = error[key];
  }
  
  return error?.message;
}
