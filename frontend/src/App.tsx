import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import { CircularProgress, Container, ThemeProvider, createTheme } from "@mui/material";

import axios from "axios";

import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";

import routes from "./routes/main/config";

const theme = createTheme({
  typography: {
    fontFamily: [
      "Noto Sans",
      "Ubuntu",
      "Roboto",
      "times new roman",
      "times",
      "roman",
      "serif",
    ].join(","),
  },
    palette: {
      mode: 'dark',
    }
  // palette: {
  //   primary: {
  //     light: "#D5E1DB",
  //     main: "#000F08",
  //     dark: "",
  //     contrastText: "",
  //   },
  //   secondary: {
  //     light: "",
  //     main: "",
  //     dark: "",
  //     contrastText: "",
  //   }
  // }
});

const loadingFallBack = (
  <Container maxWidth="sm" sx={{ display: 'flex', justifyContent: 'center'}}>
    <CircularProgress size="min(min(15vh, 15vw), 500px)" />
  </Container>
);
const router = createBrowserRouter(routes);

const App = () => {
  axios.defaults.xsrfCookieName = 'csrftoken';
  axios.defaults.xsrfHeaderName = 'X-CSRFToken';
  
  return (
    <React.Suspense fallback={loadingFallBack}>
      <ThemeProvider theme={theme}>
        <RouterProvider router={router}/>
      </ThemeProvider>
    </React.Suspense>
  );
};

export default App;
