import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "@fontsource/roboto";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/400-italic.css";
import {
  CircularProgress,
  Container,
  createTheme,
} from "@mui/material";
import { 
  StyledEngineProvider,
  ThemeProvider
 } from "@mui/material/styles";

import axios from "axios";

import routes from "./routes/main/config";

// Update the Typography's variant prop options
declare module '@mui/material/Typography' {
  interface TypographyPropsVariantOverrides {
    h5: false;
    h6: false;
  }
}

const theme = createTheme({
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
  },
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
    mode: "light",
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
        <ThemeProvider theme={theme}>
          <RouterProvider router={router} />
        </ThemeProvider>
      </StyledEngineProvider>
    </React.Suspense>
  );
};

export default App;
