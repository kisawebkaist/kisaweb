import type { CategoryT } from "../../API/links";
import { ListItemButton } from "@mui/material";

type CategoryEntry = {
  data: CategoryT;
  id: number;
  isActiveCategory: (category: CategoryT) => boolean;
  setActiveCategory: (id: number) => void;
};

const LinkCategory = ({ data, isActiveCategory, setActiveCategory }: CategoryEntry) => {
  const isActive = isActiveCategory(data);
  return (
    <ListItemButton
      selected = {isActive}
      onClick = {() => setActiveCategory(data.id)}
    >
      {data.title_category}
    </ListItemButton>
  );
};

export default LinkCategory;
