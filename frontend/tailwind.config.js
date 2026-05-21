/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: ["./*.{html,js}"],
  theme: {
    extend: {
      colors: {
        "on-primary-fixed-variant": "#004f4f",
        "on-tertiary-fixed": "#291800",
        "on-primary-fixed": "#002020",
        "on-background": "#e0e3e5",
        "surface-dim": "#101415",
        "on-primary": "#003737",
        "surface-container-high": "#272a2c",
        "on-surface-variant": "#bacac9",
        "tertiary": "#ffd498",
        "on-tertiary": "#442b00",
        "secondary-fixed-dim": "#bbc7df",
        "outline": "#859493",
        "inverse-primary": "#006a6a",
        "on-surface": "#e0e3e5",
        "surface-container": "#1d2022",
        "primary": "#48f1f0",
        "primary-container": "#00d4d4",
        "tertiary-container": "#feaf1f",
        "surface-container-highest": "#323537",
        "secondary-fixed": "#d7e3fc",
        "primary-fixed": "#54f9f9",
        "on-secondary-fixed-variant": "#3c475b",
        "on-secondary-container": "#adb9d1",
        "tertiary-fixed": "#ffddb1",
        "surface": "#101415",
        "inverse-on-surface": "#2d3133",
        "surface-container-low": "#191c1e",
        "tertiary-fixed-dim": "#ffba4b",
        "on-tertiary-container": "#6a4600",
        "secondary-container": "#3e495e",
        "on-tertiary-fixed-variant": "#624000",
        "background": "#101415",
        "inverse-surface": "#e0e3e5",
        "secondary": "#bbc7df",
        "outline-variant": "#3b4949",
        "error": "#ffb4ab",
        "surface-variant": "#323537",
        "error-container": "#93000a",
        "surface-tint": "#22dcdc",
        "on-error-container": "#ffdad6",
        "on-secondary-fixed": "#101c2e",
        "surface-container-lowest": "#0b0f10",
        "surface-bright": "#363a3b",
        "primary-fixed-dim": "#22dcdc",
        "on-primary-container": "#005757",
        "on-error": "#690005"
      },
      borderRadius: {
        "DEFAULT": "0.25rem",
        "lg": "0.5rem",
        "xl": "0.75rem",
        "full": "9999px"
      },
      spacing: {
        "container-max": "1440px",
        "margin-mobile": "16px",
        "unit": "8px",
        "margin-desktop": "40px",
        "gutter": "24px"
      },
      fontFamily: {
        "headline-lg": ["Inter"],
        "label-sm": ["Inter"],
        "body-md": ["Inter"],
        "headline-md": ["Inter"],
        "label-md": ["Inter"],
        "body-lg": ["Inter"]
      },
      fontSize: {
        "headline-lg": ["40px", {"lineHeight": "1.2", "letterSpacing": "-0.02em", "fontWeight": "700"}],
        "label-sm": ["12px", {"lineHeight": "1", "fontWeight": "600"}],
        "body-md": ["16px", {"lineHeight": "1.5", "fontWeight": "400"}],
        "headline-md": ["22px", {"lineHeight": "1.3", "fontWeight": "600"}],
        "label-md": ["14px", {"lineHeight": "1.4", "letterSpacing": "0.01em", "fontWeight": "500"}],
        "body-lg": ["18px", {"lineHeight": "1.6", "fontWeight": "400"}]
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/container-queries')
  ],
}
