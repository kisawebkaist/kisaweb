import {
  useRoutes
} from "react-router-dom"
import mainConfig from './main/config'

const KisaRouter = () => {
  const mainRoutes = useRoutes(mainConfig)
  return mainRoutes
}

export default KisaRouter
