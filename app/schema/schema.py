from ariadne import make_executable_schema, load_schema_from_path
from app.schema.query import query
from app.schema.mutation import mutation

type_def = load_schema_from_path("app/schema/type_defs.graphql")

schema = make_executable_schema(type_def, query, mutation)