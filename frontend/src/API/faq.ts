export type FaqT = {
  question : string
  timestamp : string // Datetime string
  category : number // Primary Key
  answer : string
  id : number
}

export type CategoryT = {
  title_category : string
  title_slug : string
  id : number
}

export default class FaqAPI{
  static allFaqs = <T extends Record<string, any> >(
    queryParams : T
  ) : Promise<FaqT[]> => {

  }
  static allCategories = <T extends Record<string, any> >(
    queryParams : T
  ) : Promise<CategoryT[]> => {

  }
}
