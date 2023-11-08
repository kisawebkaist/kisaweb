import { CategoryT, FaqT } from "../API/faq";
import FaqAPI from "../API/faq";
import QueryGuard from "../components/query-guard";
import React from "react";

// Define the expected types for faqs and categories
type FaqP = {
  faqs: FaqT[];
  categories: CategoryT[];
};

const Faq = ({ faqs, categories }: FaqP) => {
  return (
    <React.Fragment>
      <p>Test</p>
    </React.Fragment>
  );
}

const FaqWithGuard = () => {
  const query = React.useCallback<() => Promise<FaqP>>(
    async () => {
      const faqs = await FaqAPI.allFaqs({});
      const categories = await FaqAPI.allCategories({});
      
      // Return the data in the expected format
      return {
        faqs: faqs,
        categories: categories,
      };
    },
    []
  );

  return (
    <QueryGuard
      render={Faq}
      props={{}}
      query={query}
      args={undefined}
      fallback={<>404 LOL</>}
    />
  );
}

export default FaqWithGuard;