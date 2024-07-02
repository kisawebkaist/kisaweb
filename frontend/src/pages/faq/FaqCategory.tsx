import type { CategoryT } from "../../API/faq";
import { ListItemButton, ListItemText } from "@mui/material";

type CategoryEntry = {
  data: CategoryT;
  id: number;
  isActiveCategory: (category: CategoryT) => boolean;
  setActiveCategory: (id: number) => void;
};

const FaqCategory = ({
  data,
  isActiveCategory,
  setActiveCategory,
}: CategoryEntry) => {
  const isActive = isActiveCategory(data);
  return (
    <ListItemButton
      onClick={() => setActiveCategory(data.id)}
      selected={isActive}
    >
      <ListItemText>
        {data.title_category}
      </ListItemText>
    </ListItemButton>
  );
};

export default FaqCategory;
