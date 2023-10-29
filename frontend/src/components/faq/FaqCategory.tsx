import type { CategoryT } from "../../API/faq";
import { Typography } from "@mui/material";

type CategoryEntry = {
  data: CategoryT;
  id: number;
  isActive: boolean;
  onChoose: () => void;
};

const FaqCategory = ({ data, isActive, onChoose }: CategoryEntry) => {
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
      onClick={onChoose}
    >
      {data.title_category}
    </Typography>
  );
};

export default FaqCategory;
