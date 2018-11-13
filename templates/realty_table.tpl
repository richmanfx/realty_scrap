<!doctype html>
<html lang="ru">
    <head>
    	<meta charset="utf-8">
        <title>Realty</title>
        <link rel="stylesheet" type="text/css" href="css/qa.css">
    </head>


    <body>
    	<h1>Объекты недвижимости</h1>

        <table border="1">
            {% for realty_object_string in realty_objects_array %}
            <tr>
                <td>{{realty_object_string[1]}}</td>
                <td>{{realty_object_string[2]}}</td>
                <td>{{realty_object_string[3]}}</td>
                <td>{{realty_object_string[4]}}</td>
                <td>{{realty_object_string[5]}}</td>
                <td>{{realty_object_string[6]}}</td>
                <td>{{realty_object_string[7]}}</td>
                <td>{{realty_object_string[8]}}</td>
                <td>{{realty_object_string[9]}}</td>
                <td>{{realty_object_string[10]}}</td>
                <td>{{realty_object_string[11]}}</td>
            </tr>
            {% endfor %}
        </table>

    </body>
</html>
