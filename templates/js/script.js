/**
 * Created by nico on 8/04/15.
 */

function addingredient() {
    var numIngredientsInput = document.getElementById("numIngredients");
    var numIngredients = parseInt(numIngredientsInput.getAttribute("value"));
    var nextIngredientNumber = numIngredients;

    var ingNameDiv = document.createElement("div");
    ingNameDiv.setAttribute("class", "col-md-6 column");
    var ingName = document.createElement("input");
    ingName.setAttribute("type", "text");
    ingName.setAttribute("class", "form-control");
    ingName.setAttribute("name", "ingredients" + nextIngredientNumber.toString());
    ingName.setAttribute("required", "true");
    ingName.setAttribute("placeholder", "Name");
    ingNameDiv.appendChild(ingName);

    var ingQuantityDiv = document.createElement("div");
    ingQuantityDiv.setAttribute("class", "col-md-6 column");
    var ingQuantity = document.createElement("input");
    ingQuantity.setAttribute("type", "text");
    ingQuantity.setAttribute("class", "form-control");
    ingQuantity.setAttribute("name", "quantities" + nextIngredientNumber.toString());
    ingQuantity.setAttribute("required", "true");
    ingQuantity.setAttribute("placeholder", "Quantity");
    ingQuantityDiv.appendChild(ingQuantity);

    var ingredientForm = document.createElement("div");
    ingredientForm.setAttribute("class", "form-ingredient form-group");
    ingredientForm.appendChild(document.createElement("br"));
    ingredientForm.appendChild(ingNameDiv);
    ingredientForm.appendChild(ingQuantityDiv);

    var rowDiv = document.createElement("div");
    rowDiv.setAttribute("class", "row");
    rowDiv.appendChild(ingredientForm);
    var ingredientsForm = document.getElementById("form-ingredients");
    ingredientsForm.appendChild(rowDiv);

    var newIngredientsNumber = nextIngredientNumber + 1;
    numIngredientsInput.setAttribute("value", newIngredientsNumber.toString());
}
function addstep() {
    var numStepsInput = document.getElementById("numSteps");
    var numSteps = parseInt(numStepsInput.getAttribute("value"));
    var nextStepNumber = numSteps;

    var step = document.createElement("input");
    step.setAttribute("type", "text");
    step.setAttribute("class", "form-control");
    step.setAttribute("name", "steps" + nextStepNumber.toString());
    step.setAttribute("required", "true");
    step.setAttribute("placeholder", "Instructions for this step");
    var stepsForm = document.getElementById("form-steps");
    stepsForm.appendChild(document.createElement("br"));
    stepsForm.appendChild(step);

    var newStepNumber = nextStepNumber + 1;
    numStepsInput.setAttribute("value", newStepNumber.toString());
}

function find(i) {
    $.ajax({
        url: "search",
        data: {
            chain: i
        },
        type: "GET",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data) {
            $("#search").autocomplete({
                source: data.suggestions,
                select: function (a, b) {
                    window.location.href = "recipe?id=" + b.item.data;
                }
            });
        }
    });
}

function AsyncConfirmYesNo(title, msg, yesFn) {
    var $confirm = $("#modalConfirmYesNo");
    $confirm.modal('show');
    $("#lblTitleConfirmYesNo").html(title);
    $("#lblMsgConfirmYesNo").html(msg);
    $("#btnYesConfirmYesNo").off('click').click(function () {
        yesFn();
        $confirm.modal("hide");
    });
    $("#btnNoConfirmYesNo").off('click').click(function () {
        $confirm.modal("hide");
    });
}

function ShowConfirmYesNo(message, MyYesFunction) {
    AsyncConfirmYesNo(
        "Confirmation Box",
        message,
        MyYesFunction
    );
}