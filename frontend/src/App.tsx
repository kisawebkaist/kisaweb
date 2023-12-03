import { ThemeProvider, createTheme } from "@mui/material"
import KisaRoutes from "./routes/routes"
import { BrowserRouter } from "react-router-dom"
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

const theme = createTheme({
  typography: {
    fontFamily: [
      "Ubuntu",
      "Roboto",
      "times new roman",
      "times",
      "roman",
      "serif"
    ].join(','),
  },
});

const App = () => {
  return (
    <ThemeProvider theme = {theme}>
      <BrowserRouter>
        <KisaRoutes />
      </BrowserRouter>
    </ThemeProvider>
  )
}

export default App
