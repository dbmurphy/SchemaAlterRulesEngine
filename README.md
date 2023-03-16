# SchemaChangeRiskEngine (SCRE):

A tool for assessing the risk of schema changes in a MySQL database when using tools like gh-ost or flywheel.

## The problem

Based on [Impact analysis of database schema changes](https://www.researchgate.net/publication/221555365_Impact_analysis_of_database_schema_changes)
and real world learning. It was found we should restrict riskier changes and patterns.

Such patterns include:

* BLOB & TEXT column overuse and storage/memory waste
* ENUM columns issues with casting during value parsing of a change
* SET columns issues with casting during value parsing of a change
* Foreign Key and Trigger usage preventing non-blocking and non-atomic changes
* No Primary Key causing slow migration or table level locking verses row level locking
* Renaming columns and tables leading toward application, data warehouse, and data lake sync issues

## The solution

This tool addresses this by allowing you to pass any CREATE or ALTER statement, and it will return a boolean if it's safe.

### Example

```python
from schema_change_risk_engine import SchemaChangeRiskEngine as SCRE

engine = SCRE()
changeStatements = [
    """
        CREATE TABLE `test` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `name` varchar(255) NOT NULL,
        PRIMARY KEY (`id`)
        )
        ENGINE=InnoDB
        DEFAULT CHARSET=utf8mb4
        COLLATE=utf8mb4_0900_ai_ci
    """,
    "ALTER TABLE `test` ADD COLUMN `age` int(11) NOT NULL DEFAULT 0",
    "ALTER TABLE `test` RENAME COLUMN `age` to `years_old`",
    "ALTER TABLE `test` ADD COLUMN `gener` ENUM('M', 'F','T','NC') NOT NULL DEFAULT 'NC'",
    "ALTER TABLE `test` ADD COLUMN `hobbies` SET('S', 'R','T','NC') NOT NULL DEFAULT 'NC'",
    "ALTER TABLE `test` ADD COLUMN `bio` TEXT NOT NULL",
    "ALTER TABLE `test` ADD COLUMN `photo` BLOB NOT NULL",
    "ALTER TABLE `test` ADD COLUMN `order_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "ALTER TABLE `test` ADD TRIGGER `test_trigger` AFTER INSERT ON `test` FOR EACH ROW BEGIN INSERT INTO `test` (`name`) VALUES ('test'); END",
    "ALTER TABLE `test` ADD FOREIGN KEY (`id2`) REFERENCES `test` (`id`)",
    "ALTER TABLE `test` RENAME TO `test2`",
    "ALTER TABLE `test` RENAME TABLE `test2` TO `test`"
]

> for idx, change in enumerate(changeStatements):
    print("Statement %s: %s" % (idx + 1, engine.validate(change)))

Statement
1: (True, None)
Statement
2: (True, None)
Statement
3: (False, 'Renaming columns is not allowed')
Statement
4: (False, 'ENUM data type is not allowed')
Statement
5: (False, 'SET is not allowed')
Statement
6: (False, 'TEXT columns are not allowed')
Statement
7: (False, 'BLOB columns are not allowed')
Statement
8: (False, 'DATETIME data type is not allowed')
Statement
9: (False, 'Triggers are not allowed')
Statement
10: (False, 'Foreign keys are not allowed')
Statement
11: (False, 'Renaming tables is not allowed')
Statement
12: (False, 'Renaming tables is not allowed')



```
