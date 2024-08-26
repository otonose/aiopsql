<h1>Asynchronous PostgreSQL Database Interaction</h1>

<p><strong>An asynchronous Python database application that leverages SQLAlchemy ORM for seamless interaction with PostgreSQL databases.</strong></p>

<h2>Installation</h2>

<p>To install this package, clone the repository and install the required dependencies:</p>

<pre><code>git clone https://github.com/otonose/py-aiopsql.git
cd py-aiopsql
pip install -r requirements.txt
</code></pre>

<h2>Usage</h2>

<h3>Configuration</h3>

<p>Before using this package, ensure that your database configuration is set up correctly. You can specify your configuration in your code or via environment variables.</p>

<pre><code>from async_db_postgresql import AsyncDatabase

db = AsyncDatabase(
    dialect="postgresql",
    user="yourusername",
    password="yourpassword",
    host="localhost",
    port=5432,
    database_name="yourdatabase"
)
</code></pre>

<h3>Basic Examples</h3>

<h4>Selecting Data</h4>

<pre><code>from async_db_postgresql import db

async def fetch_data():
    results = await db.select(SomeModel, where_clause=SomeModel.column == 'value')
    print(results)
</code></pre>

<h4>Inserting Data</h4>

<pre><code>from async_db_postgresql import db

async def insert_data():
    await db.insert(SomeModel, values_params=[{"column1": "value1", "column2": "value2"}])
</code></pre>

<h4>Updating Data</h4>

<pre><code>from async_db_postgresql import db

async def update_data():
    await db.update(SomeModel, where_clause=SomeModel.id == 1, value_params={"column": "new_value"})
</code></pre>

<h4>Deleting Data</h4>

<pre><code>from async_db_postgresql import db

async def delete_data():
    await db.delete(SomeModel, where_clause=SomeModel.id == 1)
</code></pre>
