import { CategoryT, FaqT } from "../API/faq"
import QueryGuard from "../components/query-guard"
import React from "react"

type FaqP = {
  faqs : FaqT,
  categories : CategoryT
}

const Faq = ({faqs, categories} : FaqP) => {
  return (
    <React.Fragment>

    </React.Fragment>
  )
}

const FaqWithGuard = () => {
  const query = React.useCallback<(params : undefined) => Promise<FaqP> >(
    (params : undefined) => {

    }, []
  )
  return (
    <QueryGuard
      render = {Faq}
      props = {{}}
      query = {query}
      args = {undefined}
      fallback = {<>404 LOL</>}
    />
  )
}

export default FaqWithGuard
