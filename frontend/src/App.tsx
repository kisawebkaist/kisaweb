import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "@fontsource/roboto";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/400-italic.css";
import {
  CircularProgress,
  Container,
} from "@mui/material";
import { 
  experimental_extendTheme as extendTheme,
  Experimental_CssVarsProvider as CssVarsProvider,
  StyledEngineProvider } from "@mui/material/styles";

import axios from "axios";

import routes from "./routes/main/config";

// Update the Typography's variant prop options
declare module '@mui/material/Typography' {
  interface TypographyPropsVariantOverrides {
    h5: false;
    h6: false;
    fancy_h1: true;
    fancy_h2: true;
    fancy_h3: true;
    fancy_h4: true;
  }
}

declare module '@mui/material/styles' {
  interface TypographyVariants {
    fancy_h1: React.CSSProperties;
    fancy_h2: React.CSSProperties;
    fancy_h3: React.CSSProperties;
    fancy_h4: React.CSSProperties;
  }

  // allow configuration using `createTheme`
  interface TypographyVariantsOptions {
    fancy_h1?: React.CSSProperties;
    fancy_h2?: React.CSSProperties;
    fancy_h3?: React.CSSProperties;
    fancy_h4?: React.CSSProperties;
  }
}

const theme = extendTheme({
  typography: {
    fontFamily: ["Itim", "Roboto", "times", "roman", "serif"].join(","),
    // copied it from mui default h3-6
    h1: {
      fontWeight: 400,
      fontSize: "3rem",
      lineHeight: 1.167,
      letterSpacing: "0em",
    },
    h2: {
      fontWeight: 400,
      fontSize: "2.125rem",
      lineHeight: 1.235,
      letterSpacing: "0.00735em",
    },
    h3: {
      fontWeight: 400,
      fontSize: "1.5rem",
      lineHeight: 1.334,
      letterSpacing: "0em",
    },
    h4: {
      fontWeight: 500,
      fontSize: "1.25rem",
      lineHeight: 1.6,
      letterSpacing: "0.0075em",
    },
    fancy_h1: {
      fontFamily: "Satisfy",
      fontWeight: 400,
      fontSize: "3rem",
      lineHeight: 1.167,
      letterSpacing: "0em",
    },
    fancy_h2: {
      fontFamily: "Satisfy",
      fontWeight: 400,
      fontSize: "2.125rem",
      lineHeight: 1.235,
      letterSpacing: "0.00735em",
    },
    fancy_h3: {
      fontFamily: "Satisfy",
      fontWeight: 400,
      fontSize: "1.5rem",
      lineHeight: 1.334,
      letterSpacing: "0em",
    },
    fancy_h4: {
      fontFamily: "Satisfy",
      fontWeight: 500,
      fontSize: "1.25rem",
      lineHeight: 1.6,
      letterSpacing: "0.0075em",
    },
  },
  colorSchemes: {
    light: {
      palette: {
        primary: {
          main: "#43bFF8",
        },
        secondary: {
          main: "#f87c43",
        },
        background : {
          default : "#f1f5f9",
          paper : "#f8fafc"
        },
      }
    }
  },
  components: {
    MuiAccordionSummary: {
      defaultProps: {
        sx: {flexDirection: 'row-reverse'}
      }
    }
  },
});

const loadingFallBack = (
  <Container sx={{ display: "flex", justifyContent: "center" }}>
    <CircularProgress size="min(min(15vh, 15vw), 500px)" />
  </Container>
);
const router = createBrowserRouter(routes);

const App = () => {
  axios.defaults.xsrfCookieName = "csrftoken";
  axios.defaults.xsrfHeaderName = "X-CSRFToken";

  return (
    <React.Suspense fallback={loadingFallBack}>
      <StyledEngineProvider injectFirst>
        <CssVarsProvider theme={theme}>
          <RouterProvider router={router} />
        </CssVarsProvider>
      </StyledEngineProvider>
    </React.Suspense>
  );
};

export default App;
