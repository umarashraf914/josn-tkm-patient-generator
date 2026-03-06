# Quick test for pulse rules
class MockSession(dict):
    def __getattr__(self, key):
        return self.get(key)
    def __setattr__(self, key, value):
        self[key] = value

from constraints.pulse_rules import apply_pulse_rules

# Test with 요통 기허형 (허증)
session = MockSession()
session['disease'] = '요통'
session['pattern_idx'] = 2  # 기허형 index
session['pulse_rate'] = 70

apply_pulse_rules(session)
print(f'요통 기허형 -> 맥상: {session["compound_pulse"]}, 맥박: {session["pulse_rate"]}')

# Test with 감기 풍열형
session2 = MockSession()
session2['disease'] = '감기/급성상기도감염'
session2['pattern_idx'] = 1  # 풍열형 index
session2['pulse_rate'] = 70

apply_pulse_rules(session2)
print(f'감기 풍열형 -> 맥상: {session2["compound_pulse"]}, 맥박: {session2["pulse_rate"]}')

# Test with 소화불량 양허형 (허증)
session3 = MockSession()
session3['disease'] = '기능성소화불량'
session3['pattern_idx'] = 3  # 양허형 index
session3['pulse_rate'] = 70

apply_pulse_rules(session3)
print(f'소화불량 양허형 -> 맥상: {session3["compound_pulse"]}, 맥박: {session3["pulse_rate"]}')

print('\n✅ Pulse rules applied successfully!')
