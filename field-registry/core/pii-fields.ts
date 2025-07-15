export const piiFields = {
  direct_identifiers: [
    'ssn', 'social_security_number', 'driver_license',
    'passport_number', 'bank_account', 'credit_card'
  ],
  quasi_identifiers: [
    'first_name', 'last_name', 'email', 'phone',
    'date_of_birth', 'zip_code', 'address'
  ],
  sensitive_data: [
    'income', 'debt_amount', 'medical_conditions',
    'employment_status', 'credit_score'
  ]
};

export function isPIIField(fieldName: string): boolean {
  return Object.values(piiFields).some(fields => 
    fields.includes(fieldName)
  );
}
