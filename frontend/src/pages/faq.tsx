import { CategoryT, FaqT } from "../API/faq"
import FaqAPI from "../API/faq"
import QueryGuard from "../components/query-guard"
import React from "react"

type FaqP = {
  faqs : FaqT,
  categories : CategoryT
}

const Faq = ({faqs, categories} : FaqP) => {
  return (
    <React.Fragment>
      <p>test<p/>
    </React.Fragment>
  )
}

const FaqWithGuard = () => {
  const query = React.useCallback<() => Promise<FaqP>>(
    async () => {
      const faqs = await FaqAPI.allFaqs({});
      const categories = await FaqAPI.allCategories({});
      
      return {
        faqs,
        categories,
      };
    },
    []
  );

export default FaqWithGuard
