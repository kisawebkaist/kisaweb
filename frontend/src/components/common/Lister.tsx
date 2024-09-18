import { RenderElementTypeT } from "./common"
import React from "react"

type ListerChildP<T, U> = {
  data : T,
  id : number
} & U

type ListerP<T, U> = {
  array: T[],
  render: RenderElementTypeT<ListerChildP<T, U>>,
  props: U,
  getKey?: (value: T) => string,
}

function genRandomString(length : number) {
   let chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()';
   let charLength = chars.length;
   let result = '';
   for ( let i = 0; i < length; i++ ) {
      result += chars.charAt(Math.floor(Math.random() * charLength));
   }
   return result;
}

const Lister = <T, U>({array, render : Component, props, getKey } : ListerP<T, U>) => {
  const elements = React.useMemo(() => {
    return array.map((data, id) => {
      const renderProps = {
        data, id, ...props, key : getKey? getKey(data) : id
      } as ( React.PropsWithRef<ListerChildP<T, U>> & ListerChildP<T, U> )
      return (
        <Component {...renderProps}/>
      )
    })
  }, [array, props, getKey, Component])
  return (
    <>{elements}</>
  )
}

export default Lister
