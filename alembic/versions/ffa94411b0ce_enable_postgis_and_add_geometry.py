from alembic import op
import sqlalchemy as sa
from geoalchemy2.types import Geometry

def upgrade():
    # Enable PostGIS extension first
    op.execute('CREATE EXTENSION IF NOT EXISTS postgis')
    
    # Then create the table with geometry column
    op.create_table('stations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('code', sa.String()),
        sa.Column('geom', Geometry(geometry_type='POINT', srid=4326)),
        sa.Column('address', sa.String()),
        sa.Column('station_type', sa.String()),
        sa.Column('wheelchair_accessible', sa.Boolean()),
        sa.Column('is_active', sa.Boolean()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )
    
    # Create spatial index
    op.create_index('idx_stations_geom', 'stations', ['geom'], 
                   postgresql_using='gist')

def downgrade():
    op.drop_index('idx_stations_geom', table_name='stations')
    op.drop_table('stations')
    op.execute('DROP EXTENSION IF EXISTS postgis')