import json_manager
import click

@click.group()
def cli():
    pass

@cli.command()
def users():
    users = json_manager.read_json()
    for user in users:
        print(f"{user['id']} - {user['name']} {user['lastname']}")

@cli.command()
@click.argument("id", type=int)
def user(id):
    users = json_manager.read_json()
    user = next((x for x in users if x["id"] == id), None)
    if user is None:
        print(f"User with id {id} not found")
    else:
        print(f"{user['id']} - {user['name']} {user['lastname']}")

@cli.command()
@click.pass_context
@click.option("--name", required=True, help="Name of the user")
@click.option("--lastname", required=True, help="Lastname of the user")
def new(ctx, name, lastname):
    if not name or not lastname:
        ctx.fail("The name and lastname are required")
    else:
        users = json_manager.read_json()
        existing_ids = set(user["id"] for user in users)
        new_id = 1
        while new_id in existing_ids:
            new_id += 1
        new_user = {
            "id": new_id,
            "name": name,
            "lastname": lastname
        }
        users.append(new_user)
        json_manager.write_json(users)
        print(f"User {name} {lastname} created successfully with id {new_id}")

@cli.command()
@click.argument("id", type=int)
@click.option("--name", help="Name of the user")
@click.option("--lastname", help="Lastname of the user")
def update(id, name, lastname):
    users = json_manager.read_json()
    for user in users:
        if user["id"] == id:
            if name is not None:
                user["name"] = name
            if lastname is not None:
                user["lastname"] = lastname
            break
    json_manager.write_json(users)
    print(f"User with id {id} updated successfully")

@cli.command()
@click.argument("id", type=int)
def delete(id):
    users = json_manager.read_json()
    user = next((x for x in users if x["id"] == id), None)
    if user is None:
        print(f"User with id {id} not found")
    else:
        users.remove(user)
        json_manager.write_json(users)
        print(f"User with id {id} delete successfully")

if __name__ == "__main__":
    cli()
