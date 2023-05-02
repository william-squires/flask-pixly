"use strict";

const BASE_URL = "http://localhost:5000"

$("#cupcakeForm").on("submit", makeCupcake);

// TODO: Add docstrings for all functions.
async function makeCupcake(evt){
  // console.log("evt=", evt);
  evt.preventDefault();

  const flavor = $("#flavor").val()
  const rating = $("#rating").val() // TODO: This is returning a string value, not an integer! (Turn into int before return server)
  const size = $("#size").val()
  const image = $("#image").val()

  const response = await axios.post(
    `${BASE_URL}/api/cupcakes`,
    data = {
      flavor,
      rating,
      size,
      image
    });
  console.log("response in submitCupcake=", response);

  // TODO: Check jQuery docs and use trigger method so we don't need to manually
  // iterate through each one individually.

  for (let field of $("#cupcakeForm")[0]) {
    field.value = "";
  }

  makeCupcakeList(); // TODO: Append to list item rather than refreshing whole list
  // after refactoring makeListItems and makeCupcakeList

}

async function getCupcakes(){
  const response = await axios.get(`${BASE_URL}/api/cupcakes`);
  console.log("response=", response);
  return response.data.cupcakes;
}

function makeListItems(cupcake){ // TODO: rename to getCupcakeHTML and refactor to return just the HTML back
  const $list_item = $("<li>").text(`${cupcake.flavor}, ${cupcake.rating},
  ${cupcake.size}`);

  const $img = $("<img>").attr("src", cupcake.image).width('200px');

  $list_item.append($img) // TODO: remove appending
}

async function makeCupcakeList(){
  $(".cupcakeList").empty();
  let cupcakesList = await getCupcakes();
  for(let cupcake of cupcakesList){
    console.log("cupcake in loop=", cupcake);
    $(".cupcakeList").append(makeListItems(cupcake));
  }
}

makeCupcakeList();
