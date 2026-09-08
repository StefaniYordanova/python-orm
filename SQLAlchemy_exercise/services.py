from sqlalchemy import select

from models import Recipe, Chef
from main import session
from helpers import handle_session


@handle_session(session)
def create_recipe(name: str, ingredients: str, instructions: str):
    session.add(Recipe(name=name, ingredients=ingredients, instructions=instructions))


@handle_session(session)
def update_recipe_by_name(name: str, new_name: str,  new_ingredients: str, new_instructions: str) -> None:
    session.execute(
        update(Recipe)
        .where(Recipe.name == name)
        .values(
            name=new_name,
            ingredients=new_ingredients,
            instructions=new_instructions
        )
    )


@handle_session(session)
def delete_recipe_by_name(name: str) -> None:
    # session.query(Recipe).filter_by(name=name).delete()
    session.execute(
        delete(Recipe).where(Recipe.name == name)
    )


@handle_session(session)
def get_recipes_by_ingredient(ingredient_name: str):
    # session.query(Recipe).filter(Recipe.ingredients.ilike(f'%{ingredient_name}%')).all()
    return session.scalars(
        select(Recipe).where(
            Recipe.ingredients.ilike(f'%{ingredient_name}%')
        )
    ).all()


@handle_session(session)
def swap_recipe_ingredients_by_name(first_recipe_name: str, second_recipe_name: str):
    first_recipe = session.scalars(
        select(Recipe)
        .where(Recipe.name == first_recipe_name)
        .with_for_update()
    ).one()

    second_recipe = session.scalars(
        select(Recipe)
        .where(Recipe.name == second_recipe_name)
        .with_for_update()
    ).one()

    first_recipe.ingredients, second_recipe.ingredients = second_recipe.ingredients, first_recipe.ingredients


@handle_session(session)
def relate_recipe_with_chef_by_name(recipe_name: str, chef_name: str) -> str:
    recipe = session.scalars(
        select(Recipe)
        .where(Recipe.name == recipe_name)
    ).one()

    if recipe.chef:
        raise Exception(f"Recipe: {recipe.name} already has a related chef")

    chef = session.scalars(
        select(Chef)
        .where(Chef.name == chef_name)
    ).one()

    recipe.chef = chef
    return f"Related recipe {recipe_name} with chef {chef_name}"


@handle_session(session)
def get_recipes_with_chef() -> str:
    recipes = session.execute(
        select(Recipe.name, Chef.name)
        .join(Recipe.chef)
    )

    return '\n'.join(
        f"Recipe: {recipe_name} made by chef: {chef_name}"
        for recipe_name, chef_name in recipes
    )

