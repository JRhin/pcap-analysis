"""Pydantic model to handle a pyshark.packet.

The model convert basically all the entries in integers (beside 'src' and 'dst' which are saved as string, and the 'sniff_timestamp' which is saved as float)

There are also two validators:
    - flags_rb_must_be_zero : which check that flags_rb is always equal to 0.
    - set_dsfield_int16 : which convert the dsfield in a integer base 16.
"""

from pydantic import BaseModel, validator, ValidationError

# Pydantic class for validatiion of a packet
class Packet(BaseModel):
    # Label of DSCP
    dsfield_dscp: int
    # Header Length
    hdr_len: int
    # Differentiated Service
    dsfield: int
    # Explicit Congestion Notification
    dsfield_ecn: int
    # Length of the Packet including header
    len: int
    # Number of Protocol
    proto: int
    # Flag Do not Fragment
    flags_df: int
    # Flag More Fragment
    flags_mf: int
    # Flag Reserved - Must be 0
    flags_rb: int
    # Fragment Offset
    frag_offset: int
    # Time To Live
    ttl: int
    # Source Address
    src: str
    # Destination Address
    dst: str
    # Source port
    srcport: int
    # Destination port
    dstport: int
    # Time
    sniff_timestamp: float

    @validator('flags_rb')
    def flags_rb_must_be_zero(cls,
                              v: int) -> int:
        if v != 0:
            raise ValidationError('flags_rb must be zero.')
        return v

    @validator('dsfield', pre=True)
    def set_dsfield_int16(cls,
                          v: str) -> int:
        return int(v, 16)
