import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "@fontsource/roboto";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/400-italic.css";
import {
  CircularProgress,
  Container,
} from "@mui/material";
import { ThemeProvider, StyledEngineProvider } from '@mui/material/styles';
import axios from "axios";

import routes from "./configs/routes";
import { theme } from "./core/theme";

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
