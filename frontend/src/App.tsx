import KisaRoutes from "./routes/routes"
import { BrowserRouter } from "react-router-dom"
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';


const App = () => {
  return (
    <BrowserRouter>
      <KisaRoutes />
    </BrowserRouter>
  )
}

export default App
