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

export default class FaqAPI {
  static allFaqs = <T extends Record<string, any>>(
    queryParams: T
  ): Promise<FaqT[]> => {
    // create fake data for frontend development
    const fakeFaqs: FaqT[] = [
      {
        question: "Question1",
        timestamp: "2023-11-05T12:00:00Z",
        category: 1,
        answer: "Answer1",
        id: 1,
      },
      {
        question: "Question2",
        timestamp: "2023-11-05T14:30:00Z",
        category: 2,
        answer: "Answer2",
        id: 2,
      },
    ];

    return Promise.resolve(fakeFaqs);
  };

  static allCategories = <T extends Record<string, any>>(
    queryParams: T
  ): Promise<CategoryT[]> => {
    // Generate fake CategoryT data
    const fakeCategories: CategoryT[] = [
      {
        title_category: "Title1",
        title_slug: "test1",
        id: 1,
      },
      {
        title_category: "Title2",
        title_slug: "test2",
        id: 2,
      },
    ];

    return Promise.resolve(fakeCategories);
  };
}
