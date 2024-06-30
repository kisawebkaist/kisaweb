import React from "react";
import FaqAPI, { CategoryT, FaqT } from "../API/faq";
import FaqCategory from "../components/faq/FaqCategory";
import FaqHeader from "../components/faq/FaqHeader";
import FaqQuestion from "../components/faq/FaqQuestion";
import FaqSearch from "../components/faq/FaqSearch";
import QueryGuard from "../components/query-guard";
import { Typography, Stack, List } from "@mui/material";
import { Container, Box } from "@mui/system";
import Lister from "../components/lister";
import QueryFallback from "../components/QueryFallback";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faDropbox } from "@fortawesome/free-brands-svg-icons";

// Define the expected types for faqs and categories
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

  const qnaContents = React.useMemo(() => {
    if (filteredFaqs.length !== 0)
      return <Lister array={filteredFaqs} render={FaqQuestion} props={{}} />
    return (
      <Stack className = 'h-80 opacity-50'>
        <FontAwesomeIcon icon = {faDropbox} size = "5x" className = "mb-4"/>
        <Typography variant="body2" textAlign="center" className = "text-5xl">
          No Questions Yet
        </Typography>
      </Stack>
    )

  }, [ filteredFaqs ])

  const isActiveCategory = (category: CategoryT) => {
    return activeCategory === category.id;
  };
  return (
    <Container className="">
      {/* Header */}
      <FaqHeader />
      {/* Search */}
      <FaqSearch onSearch={setSearchText} />
      <Stack
        direction = "row"
        justifyContent="space-between"
        gap={5}
      >
        {/* Categories */}
        <Box component="nav">
          <List>
            <Lister
              array={[generalCategory, ...categories]}
              render={FaqCategory}
              props={{
                isActiveCategory,
                setActiveCategory,
              }}
            />
          </List>
        </Box>
        {/* Questions */}
        <Box component="main" className="w-2/3">
          <Stack direction="column" gap={1}>
            {qnaContents}
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
      fallback={QueryFallback()}
    />
  );
};

export default FaqWithGuard;
