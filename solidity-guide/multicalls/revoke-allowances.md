# Revoke Allowances

Revoke Credit Account's token approvals to external contracts.

> For SDK implementation, see [Revoke Allowances](../../sdk-guide/multicalls/revoke-allowances.md).

## Why

You revoke allowances when:

- **Security incident** - Third-party contract may be compromised
- **Legacy cleanup** - Old accounts may have stale approvals from previous Gearbox versions
- **Defense in depth** - Proactively remove unnecessary approvals

Current Gearbox V3 automatically resets allowances to 1 after each interaction. However, older accounts from V2.1 may still have active allowances to external protocols.

## What

`revokeAdapterAllowances` resets token approvals from your Credit Account to specified contracts:

1. You specify which (spender, token) pairs to revoke
2. Credit Account sets allowance to 1 for each pair
3. External contracts can no longer spend those tokens

**Note:** Allowance is set to 1, not 0, due to gas optimization (writing non-zero to non-zero is cheaper than writing zero).

## How

### Basic Revocation

```solidity
import {ICreditFacadeV3Multicall} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3Multicall.sol";
import {MultiCall} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3.sol";
import {RevocationPair} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3Multicall.sol";

address creditFacade;
address creditAccount;
address uniswapAdapter;
address curveAdapter;
address usdc;
address dai;

// Define which approvals to revoke
RevocationPair[] memory revocations = new RevocationPair[](2);

revocations[0] = RevocationPair({
    spender: uniswapAdapter,
    token: usdc
});

revocations[1] = RevocationPair({
    spender: curveAdapter,
    token: dai
});

MultiCall[] memory calls = new MultiCall[](1);

calls[0] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.revokeAdapterAllowances,
        (revocations)
    )
});

ICreditFacadeV3(creditFacade).multicall(creditAccount, calls);
```

### Check Existing Allowances

Before revoking, check what allowances exist:

```solidity
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

// Check allowance from Credit Account to a spender
uint256 allowance = IERC20(tokenAddress).allowance(creditAccount, spenderAddress);

if (allowance > 1) {
    // Credit Account has active allowance to this spender
    // Consider revoking it
}
```

### Revoke All Adapter Allowances for a Token

```solidity
// Get all adapters from Credit Manager
address[] memory adapters = ICreditManagerV3(creditManager).adapters();

// Build revocations for all adapters
RevocationPair[] memory revocations = new RevocationPair[](adapters.length);

for (uint256 i = 0; i < adapters.length; i++) {
    revocations[i] = RevocationPair({
        spender: adapters[i],
        token: tokenAddress
    });
}

MultiCall[] memory calls = new MultiCall[](1);

calls[0] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.revokeAdapterAllowances,
        (revocations)
    )
});

ICreditFacadeV3(creditFacade).multicall(creditAccount, calls);
```

### Emergency Revocation Pattern

For security incidents, revoke immediately:

```solidity
contract EmergencyRevoke {
    ICreditFacadeV3 public creditFacade;

    function emergencyRevokeAll(
        address creditAccount,
        address compromisedAdapter,
        address[] calldata tokens
    ) external {
        RevocationPair[] memory revocations = new RevocationPair[](tokens.length);

        for (uint256 i = 0; i < tokens.length; i++) {
            revocations[i] = RevocationPair({
                spender: compromisedAdapter,
                token: tokens[i]
            });
        }

        MultiCall[] memory calls = new MultiCall[](1);
        calls[0] = MultiCall({
            target: address(creditFacade),
            callData: abi.encodeCall(
                ICreditFacadeV3Multicall.revokeAdapterAllowances,
                (revocations)
            )
        });

        creditFacade.multicall(creditAccount, calls);
    }
}
```

## Gotchas

### Usually Not Needed in V3

Gearbox V3 automatically resets allowances after each adapter interaction. This function exists mainly for:

1. Legacy accounts migrated from V2.1
2. Paranoid security posture
3. Specific incident response

If you're using a fresh V3 account, allowances are already minimal.

### RevocationPair Struct Format

The struct has two fields:

```solidity
struct RevocationPair {
    address spender;  // Contract that has the allowance
    address token;    // Token that was approved
}
```

Both must be valid addresses. Invalid addresses may cause the call to revert or have no effect.

### Sets to 1, Not 0

For gas efficiency, allowances are set to 1 instead of 0:

```solidity
// Before revocation: allowance = 1000000000000000000 (1 token)
// After revocation:  allowance = 1 (essentially zero for practical purposes)
```

An allowance of 1 wei is functionally zero for any realistic token amount.

### Can't Revoke Non-Existent Allowances

Revoking an allowance that doesn't exist (already 0 or 1) is a no-op - it won't revert, but wastes gas:

```solidity
// If allowance is already 0 or 1, this does nothing but costs gas
revocations[0] = RevocationPair({
    spender: adapterWithNoAllowance,
    token: token
});
```

### Adapter vs External Contract

Revocations target the **spender** (usually an adapter), not the underlying protocol:

```solidity
// The adapter has the allowance, not Uniswap directly
RevocationPair({
    spender: uniswapAdapter,  // Adapter address, not Uniswap Router
    token: usdcAddress
});
```

Adapters are what actually interact with your Credit Account's tokens.

### Batch Multiple Revocations

You can revoke multiple (spender, token) pairs in one call:

```solidity
// Efficient - single call with multiple revocations
RevocationPair[] memory revocations = new RevocationPair[](3);
revocations[0] = RevocationPair({spender: adapter1, token: usdc});
revocations[1] = RevocationPair({spender: adapter1, token: dai});
revocations[2] = RevocationPair({spender: adapter2, token: usdc});

// Less efficient - multiple multicalls
// Don't do this if you can batch them together
```

### When to Actually Use This

Real scenarios where revocation makes sense:

1. **Third-party exploit:** A protocol Gearbox integrates with gets hacked. Revoke allowances to that protocol's adapter as a precaution.

2. **Account migration:** Moving from V2.1 account with old allowances to ensure clean state.

3. **Compliance requirement:** Some regulatory frameworks require revoking unused approvals.

4. **Personal security policy:** You want explicit control over all approvals.

For normal operations, V3's automatic reset is sufficient.

## See Also

- [Making External Calls](./making-external-calls.md) - How adapters use allowances
- [Enabling/Disabling Tokens](./enabling-disabling-tokens.md) - Related account management
