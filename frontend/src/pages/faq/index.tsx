import React from "react";
import FaqAPI, { CategoryT, FaqT } from "../../API/faq";
import FaqCategory from "./FaqCategory";
import FaqHeader from "./FaqHeader";
import FaqQuestion from "./FaqQuestion";
import FaqSearch from "./FaqSearch";
import { Typography, Stack, List } from "@mui/material";
import { Container, Box, Grid } from "@mui/system";
import Lister from "../../components/common/Lister";
import QueryFallback from "../../components/common/QueryFallback";
import QueryGuard from "../../components/common/QueryGuard";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faComment } from "@fortawesome/free-solid-svg-icons";

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
      <Stack justifyContent="center" direction = "column">
        <FontAwesomeIcon icon = {faComment} />
        <Typography variant="body2" textAlign="center">
          No Questions Yet
        </Typography>
      </Stack>
    )

  }, [ filteredFaqs ])

  const isActiveCategory = (category: CategoryT) => {
    return activeCategory === category.id;
  };
  return (
    <Container>
      {/* Header */}
      <FaqHeader />
      {/* Search */}
      <FaqSearch onSearch={setSearchText} />
      <Grid container>
        {/* Categories */}
        <Grid component="nav" size={2}>
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
        </Grid>
        {/* Questions */}
        <Grid component="main" size={10}>
          <Stack direction="column" gap={1}>
            {qnaContents}
          </Stack>
        </Grid>
      </Grid>
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
