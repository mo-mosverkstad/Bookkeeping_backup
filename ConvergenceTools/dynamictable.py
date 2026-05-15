from typing import Dict, Iterator, Tuple

class DynamicTable:
    def __init__(self):
        self.table: Dict[str, Dict] = {}
        
    def insert_row(self, key: str, row: Dict) -> None:
        if key in self.table:
            self.table[key].update(row)
        else:
            self.table[key] = row.copy()
        
    def get_row(self, key: str) -> Dict:
        return self.table[key]
        
    def delete_row(self, key: str) -> None:
        del self.table[key]
        
    def blit(self, other: "DynamicTable") -> None:
        for other_key, other_row in other:
            self.insert_row(other_key, other_row)

    def __iter__(self) -> Iterator[Tuple[str, Dict]]:
        return iter(self.table.items())
        
    def __repr__(self) -> str:
        return f"DynamicTable({self.table})"
        
dynamic_table1: DynamicTable = DynamicTable()
dynamic_table1.insert_row("A", {"a" : 12, "b": 39})
dynamic_table1.insert_row("B", {"a" : 71, "b": 31})
dynamic_table1.insert_row("C", {"a" : 22, "b": 13})
dynamic_table1.insert_row("D", {"a" : 72, "b": 37})
dynamic_table1.insert_row("E", {"a" : 21, "b": 31})
dynamic_table1.insert_row("F", {"a" : 21, "b": 30})

dynamic_table2: DynamicTable = DynamicTable()
dynamic_table2.insert_row("A", {"b": 98, "c": 120})
dynamic_table2.insert_row("C", {"a" : 33, "b": 44, "d": 720})
dynamic_table2.insert_row("E", {"a" : 52, "c": 31})
dynamic_table2.insert_row("F", {"b" : 33, "d": 30})

print(dynamic_table1)
print(dynamic_table2)

dynamic_table1.blit(dynamic_table2)
print(dynamic_table1)
print(dynamic_table2)