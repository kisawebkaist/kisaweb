import FaqAPI, { CategoryT, FaqT } from "../API/faq";
import FaqCategory from "../components/faq/FaqCategory";
import FaqHeader from "../components/faq/FaqHeader";
import FaqQuestion from "../components/faq/FaqQuestion";
import FaqSearch from "../components/faq/FaqSearch";
import QueryGuard from "../components/query-guard";
import React from "react";
import { Typography, Stack } from "@mui/material";
import { Container, Box } from "@mui/system";
import Lister from "../components/lister";

type FaqP = {
  faqs: FaqT[];
  categories: CategoryT[];
};

const generalCategory: CategoryT = {
  id: -1,
  title_category: "All",
  title_slug: "all_general_all",
};

const Faq = ({ faqs, categories }: FaqP) => {
  const [searchText, setSearchText] = React.useState<string>();
  const [activeCategory, setActiveCategory] = React.useState<number>(-1);
  const [filteredFaqs, setFilteredFaqs] = React.useState<FaqT[]>(faqs);

  React.useEffect(() => {
    setFilteredFaqs(
      faqs.filter((faq) => {
        let isAccepted = true;
        if (searchText !== undefined) {
          if (
            !(
              faq.question.toLowerCase().includes(searchText.toLowerCase()) ||
              faq.answer.toLowerCase().includes(searchText.toLowerCase())
            )
          ) {
            isAccepted = false;
          }
        }
        if (activeCategory !== -1) {
          if (faq.category !== activeCategory) {
            isAccepted = false;
          }
        }
        return isAccepted ? faq : null;
      })
    );
  }, [activeCategory, searchText, faqs]);

  const isActiveCategory = (category: CategoryT) => {
    return activeCategory === category.id;
  };
  return (
    <Container maxWidth="md">
      {/* Header */}
      <FaqHeader />
      {/* Search */}
      <FaqSearch onSearch={setSearchText} />
      <Stack direction={{
        "sm":"row",
        "xs": "column"
      }} gap={5}>
        {/* Categories */}
        <Box component="nav">
          <SectionTitle title="Categories" />
          <Stack direction="column" gap={1} alignItems={{ "sm": "flex-start", "xs": "center" }}>
            {[generalCategory, ...categories].map((category, index) => (
              <FaqCategory
                key={index}
                id={index}
                isActive={isActiveCategory(category)}
                data={category}
                onChoose={() => setActiveCategory(category.id)}
              />
            ))}
          </Stack>
        </Box>
        {/* Questions */}
        <Box component="main" sx={{ width: "100%" }}>
          <SectionTitle title="Questions" />
          <Stack direction="column" gap={1}>
            <Lister 
              array = {filteredFaqs}
              render = {FaqQuestion}
              props = {{}}
            />
            {/* {filteredFaqs.map(
              (faq, index) => (
                <FaqQuestion key={index} id={index} data={faq} />
              ),
              []
            )} */}
          </Stack>
        </Box>
      </Stack>
    </Container>
  );
};

const FaqWithGuard = () => {
  const query = React.useCallback<(params: undefined) => Promise<FaqP>>(
    async (params: undefined) => {
      const faqs = await FaqAPI.allFaqs({});
      const categories = await FaqAPI.allCategories({});
      return {
        faqs,
        categories,
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
      fallback={
        <>
          We're working on updating FAQ section for you, you can visit{" "}
          <a href="/">main page</a> meanwhile!
        </>
      }
    />
  );
};

function SectionTitle({ title }: { title: string }) {
  return (
    <Typography variant="h6" fontWeight="bold">
      {title}
    </Typography>
  );
}

export default FaqWithGuard;
