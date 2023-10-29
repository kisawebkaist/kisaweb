export type FaqT = {
  question: string;
  timestamp: string; // Datetime string
  category: number; // Primary Key
  answer: string;
  id: number;
};

export type CategoryT = {
  title_category: string;
  title_slug: string;
  id: number;
};

const mockFaqs = [
  {
    question: "Common question 1",
    timestamp: "Sat Sep 30 2023 00:27:04 GMT+0900 (Korean Standard Time)", // Datetime string
    category: 1, // Primary Key
    answer: "This is answer",
    id: 1,
  },
  {
    question: "Common question 2",
    timestamp: "Sat Sep 30 2023 00:27:04 GMT+0900 (Korean Standard Time)", // Datetime string
    category: 4, // Primary Key
    answer: "This is answer 2",
    id: 1,
  },
  {
    question: "Common question 3",
    timestamp: "Sat Sep 30 2023 00:27:04 GMT+0900 (Korean Standard Time)", // Datetime string
    category: 3, // Primary Key
    answer: "This is answer 3",
    id: 1,
  },
  {
    question: "Common question 4",
    timestamp: "Sat Sep 30 2023 00:27:04 GMT+0900 (Korean Standard Time)", // Datetime string
    category: 1, // Primary Key
    answer: "This is answer 4",
    id: 1,
  },
  {
    question: "Common question 5",
    timestamp: "Sat Sep 30 2023 00:27:04 GMT+0900 (Korean Standard Time)", // Datetime string
    category: 4, // Primary Key
    answer: "This is answer 5",
    id: 1,
  },
  {
    question: "Common question 6",
    timestamp: "Sat Sep 30 2023 00:27:04 GMT+0900 (Korean Standard Time)", // Datetime string
    category: 4, // Primary Key
    answer: "This is answer 6",
    id: 1,
  },
];

const mockCategories = [
  {
    title_category: "Events",
    title_slug: "events",
    id: 1,
  },
  {
    title_category: "Welfare",
    title_slug: "welfare",
    id: 3,
  },
  {
    title_category: "Academic",
    title_slug: "academic",
    id: 4,
  },
];

export default class FaqAPI {
  static allFaqs = <T extends Record<string, any>>(
    queryParams: T
  ): Promise<FaqT[]> => {
    return new Promise((resolve, reject) => resolve(mockFaqs));
  };
  static allCategories = <T extends Record<string, any>>(
    queryParams: T
  ): Promise<CategoryT[]> => {
    return new Promise((resolve, reject) => resolve(mockCategories));
  };
}
