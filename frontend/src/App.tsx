import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "@fontsource/roboto";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/400-italic.css";
import {
  CircularProgress,
  Container,
  ThemeProvider,
  createTheme,
} from "@mui/material";
import { StyledEngineProvider } from "@mui/material/styles";

import axios from "axios";

import routes from "./routes/main/config";

const theme = createTheme({
  typography: {
    fontFamily: ["Roboto", "times new roman", "times", "roman", "serif"].join(
      ","
    ),
  },
  palette: {
    primary: {
      main: "#43bFF8",
      light: "#B1E3FD",
      dark: "#0071bd",
      contrastText: "#FFFFFF",
    },
    secondary: {
      main: "#f87c43",
      light: "#fccfbc",
      dark: "#d15414",
      contrastText: "#faeae7",
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
