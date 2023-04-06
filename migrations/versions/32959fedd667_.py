"""empty message

Revision ID: 32959fedd667
Revises: 
Create Date: 2023-04-06 14:36:56.238291

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32959fedd667'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employees',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=False),
    sa.Column('company', sa.String(), nullable=False),
    sa.Column('lcat', sa.String(), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('termination_date', sa.Date(), nullable=True),
    sa.Column('is_team_lead', sa.Boolean(), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_employees_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_employees_id'), ['id'], unique=False)

    op.create_table('teams',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('team_lead', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['team_lead'], ['employees.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('teams', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_teams_id'), ['id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('teams', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_teams_id'))

    op.drop_table('teams')
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_employees_id'))
        batch_op.drop_index(batch_op.f('ix_employees_email'))

    op.drop_table('employees')
    # ### end Alembic commands ###
