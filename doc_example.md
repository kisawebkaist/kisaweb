# `<kisa.kaist.ac.kr/your_endpoint_name>`
## `<method_name>`
lorem ipsum brief description of what the endpoint does.
Input :
```
    {
        key_name : key_type | brief description
    }

    OR

    NO INPUT

    OR

    QUERY PARAMS //Specified here, default is assumed to be body payload
    {

    }
```
Output :
```
{
    key_name : key_type | brief description.
}
```
## `<another_method_name>`
<!-- BLA BLA BLA -->


# Typing
```
{
    string : denoting string, a series of characters
    number : denoting a number, in some cases it might be beneficial to write
      int, or float
    Array[T] : an array of objects with type T
    {key : value_type, ...} : a dictionary with entries (key, value_type)

    string | number : the value could be either a string or a number
    boolean : a yes no value

    Example :
    navigation : List[{
        name : string, type : 'link', child : []
    }]
}
```
