# Foodgram - a site for publishing and viewing recipes

## Choose Your Language

- [English](README.md)
- [Русский](README.ru.md)

---

## Project Description
**Foodgram** is a social platform for those who love cooking and sharing their culinary discoveries. On this website, users can post recipes, browse others' recipes, follow interesting authors, add favorite recipes to a shopping list, and print it for convenience when buying ingredients.

## Features
- **Recipe Publishing**: Users can share their recipes with a description of the cooking process and photos.
- **Recipe Browsing**: Users can view recipes posted by others.
- **User Subscription**: Follow recipe authors and receive notifications about new posts.
- **Shopping List**: Add recipes to a shopping list for easy compilation of necessary products.
- **Printing Shopping Lists**: Users can print their shopping lists.

## Technologies
The project is implemented using the following technologies:

- **Django** for the backend.
- **Docker** for containerization and simplifying project deployment.
- **React** for the frontend (assumed based on the description).

## How to Run the Project
Launching the project involves using Docker-compose to clone the repository, navigate to the project directory, and start the container build

<details>
<summary>Run the Project</summary>

1. Clone the repository and navigate to it in the command line:

    ```sh
    git clone https://github.com/nir0k/foodgram-project-react.git
    cd foodgram-project-react
    ```

2. Install Docker
3. Run docker-compose:

    ```sh
    docker compose up
    ```

4. Create a superuser on the first launch

    ```sh
    docker exec <backend container name> python /app/manage.py createsuperuser
    ```

</details>

## Site access
User login: http://localhost:7000/

Admin-console: http://localhost:7000/admin/

API: http://localhost:7000/api/
