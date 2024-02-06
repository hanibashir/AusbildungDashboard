"""Initial migration.

Revision ID: 3662e0475ccc
Revises: 
Create Date: 2024-02-03 00:15:14.978185

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3662e0475ccc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('AusPages')
    with op.batch_alter_table('Users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('About', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Users', schema=None) as batch_op:
        batch_op.drop_column('About')

    op.create_table('AusPages',
    sa.Column('AusPageID', sa.INTEGER(), nullable=False),
    sa.Column('Title', sa.VARCHAR(length=250), nullable=True),
    sa.Column('ImageUrl', sa.TEXT(), nullable=True),
    sa.Column('ShiftType', sa.VARCHAR(length=250), nullable=True),
    sa.Column('Duration', sa.VARCHAR(length=250), nullable=True),
    sa.Column('Certificate', sa.VARCHAR(length=250), nullable=True),
    sa.Column('FirstYearSalary', sa.INTEGER(), nullable=True),
    sa.Column('SecondYearSalary', sa.INTEGER(), nullable=True),
    sa.Column('ThirdYearSalary', sa.INTEGER(), nullable=True),
    sa.Column('FourthYearSalary', sa.INTEGER(), nullable=True),
    sa.Column('Content', sa.TEXT(), nullable=True),
    sa.Column('BestPaid', sa.BOOLEAN(), nullable=True),
    sa.Column('Popular', sa.BOOLEAN(), nullable=True),
    sa.Column('Links', sa.TEXT(), nullable=True),
    sa.Column('CategoryID', sa.INTEGER(), nullable=True),
    sa.Column('UserID', sa.INTEGER(), nullable=True),
    sa.Column('Published', sa.BOOLEAN(), nullable=True),
    sa.Column('PublishedDate', sa.DATETIME(), nullable=True),
    sa.Column('UpdatedDate', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['CategoryID'], ['Categories.CategoryID'], ),
    sa.ForeignKeyConstraint(['UserID'], ['Users.UserID'], ),
    sa.PrimaryKeyConstraint('AusPageID')
    )
    # ### end Alembic commands ###