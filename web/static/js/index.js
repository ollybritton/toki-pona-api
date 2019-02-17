const settings = {
  "indentation": 4,
}

let endpoint1Example = JSON.stringify({"word":"a","definitions":{"interj":{"meanings":["ah!","ha!","oh!","ooh!","aw!","(emotion word)"],"full_name":"interjection"}},"examples":[{"toki-pona":"a a a a!","english":"Hahaha!"}],"misc":{"notes":""},"search_result_reason":"The word supplied is the word verbatim."}, null, settings.indentation)

document.getElementById("endpointExample1").innerHTML = endpoint1Example