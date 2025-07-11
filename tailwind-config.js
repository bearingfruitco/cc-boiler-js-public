module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontSize: {
        'size-1': ['32px', { lineHeight: '1.25' }],
        'size-2': ['24px', { lineHeight: '1.375' }],
        'size-3': ['16px', { lineHeight: '1.5' }],
        'size-4': ['12px', { lineHeight: '1.5' }],
      },
      fontWeight: {
        regular: '400',
        semibold: '600',
      },
      spacing: {
        '11': '44px', // min touch target
        '12': '48px', // preferred touch target
        '14': '56px', // large touch target
      },
      screens: {
        'xs': '320px',
        'sm': '384px',
        'md': '448px',
        'lg': '512px',
        'xl': '576px',
      },
      maxWidth: {
        'xs': '320px',
        'sm': '384px',
        'md': '448px',
        'lg': '512px',
        'xl': '576px',
      },
    },
  },
  plugins: [],
}
