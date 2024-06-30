import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

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
    fontFamily: [
      "Ubuntu",
      "Roboto",
      "times new roman",
      "times",
      "roman",
      "serif",
    ].join(",")
  }
});

const loadingFallBack = (
  <Container maxWidth="sm" sx={{ display: "flex", justifyContent: "center" }}>
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
