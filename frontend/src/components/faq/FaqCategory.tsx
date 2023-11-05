import type { CategoryT } from "../../API/faq";
import { Typography } from "@mui/material";

type CategoryEntry = {
  data: CategoryT;
  id: number;
  isActiveCategory: (category: CategoryT) => boolean;
  setActiveCategory: (id: number) => void;
};

const FaqCategory = ({ data, isActiveCategory, setActiveCategory }: CategoryEntry) => {
  const isActive = isActiveCategory(data);
  return (
    <Typography
      sx={{
        color: isActive ? "#0031DF" : "#474747",
        fontWeight: isActive ? "bold" : "normal",
        transition: "opacity 0.1s ease-in",
        "&:hover": {
          cursor: "pointer",
          opacity: 0.8
        },
      }}
      onClick={() => setActiveCategory(data.id)}
    >
      {data.title_category}
    </Typography>
  );
};

export default FaqCategory;
