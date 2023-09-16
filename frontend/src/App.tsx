import KisaRoutes from "./routes/routes"
import { BrowserRouter } from "react-router-dom"

const App = () => {
  return (
    <BrowserRouter>
      <KisaRoutes />
    </BrowserRouter>
  )
}

export default App
