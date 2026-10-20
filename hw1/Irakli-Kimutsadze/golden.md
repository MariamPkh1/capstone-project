# Golden Questions . check_ordering . Irakli Kimutsadze

## g1 . Reach above Safe - warning fires
Input:    [
            {"rank":1,"name":"GTU Engineering","zone":"reach"},
            {"rank":2,"name":"TSU Law",        "zone":"safe"},
            {"rank":3,"name":"Ilia Business",  "zone":"realistic"},
          ]
Expected: {"valid": False,
           "warnings": [{"type":"reach_above_safe",
             "message":"GTU Engineering (Reach, rank 1) is listed above
                        TSU Law (Safe, rank 2)"}]}
Actual:   matches expected
Result:   PASS

## g2 . Correct ordering - no warnings
Input:    [
            {"rank":1,"name":"TSU Law",        "zone":"safe"},
            {"rank":2,"name":"Ilia Business",  "zone":"realistic"},
            {"rank":3,"name":"GTU Engineering","zone":"reach"},
          ]
Expected: {"valid": True, "warnings": []}
Actual:   {"valid": True, "warnings": []}
Result:   PASS

## g3 . Single program - always valid
Input:    [{"rank":1,"name":"TSU Law","zone":"reach"}]
Expected: {"valid": True, "warnings": []}
Actual:   {"valid": True, "warnings": []}
Result:   PASS
