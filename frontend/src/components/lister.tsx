import { RenderElementTypeT } from "./common"
import React from "react"

type ListerChildP<T, U> = {
  data : T,
  id : number
} & U

type ListerP<T, U> = {
  array : T[]
  render : RenderElementTypeT<ListerChildP<T, U>>,
  props : U
}

const Lister = <T, U>({array, render : Component, props} : ListerP<T, U>) => {
  const elements = React.useMemo(() => {
    array.map((data, id) => {
      const renderProps = {
        data, id, ...props
      } as ( React.PropsWithRef<ListerChildP<T, U>> & ListerChildP<T, U> )
      return (
        <Component {...renderProps}/>
      )
    })
  }, [ props, array, Component ])
  return (
    <>{elements}</>
  )
}

export default Lister
