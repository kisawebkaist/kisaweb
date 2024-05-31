import { ThemeProvider, createTheme } from "@mui/material";
import KisaRoutes from "./routes/routes";
import React from "react";
import { BrowserRouter } from "react-router-dom";
import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";

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

const App = () => {
  return (
    <React.Suspense fallback={<p>Loading</p>}>
      <ThemeProvider theme={theme}>
        <BrowserRouter>
          <KisaRoutes />
        </BrowserRouter>
      </ThemeProvider>
    </React.Suspense>
  );
};

export default App;
