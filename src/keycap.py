# %%
import copy

from build123d import *
from ocp_vscode import show, show_all, set_port, set_defaults, Camera, Collapse

set_port(3939)
set_defaults(
    axes=True,
    axes0=True,
    reset_camera=Camera.KEEP,
    render_joints=True,
    collapse=Collapse.ALL,
)

# %%

mbk_1u = import_step("MBK_Keycap_-_1u.step")
mbk_1u_homing = import_step("MBK_Keycap_-_1u_Homing.step")
mbk_15u = import_step("MBK_Keycap_-_1.5u.step")

# Add sprue attachment joint to 1U keycap
RigidJoint(
    "edge",
    mbk_1u,
    Location(
        mbk_1u.edges().filter_by(Axis.Y).group_by(Axis.Z)[2].sort_by(Axis.X)[-2] @ 0.5,
        (0, 180, 0)
    ),
)

# %%

keycap_wall_thickness = 1

sprue_width = 1.5
sprue_height = 2

attachment_width = keycap_wall_thickness * 2 + sprue_width
attachment_length = 1.5
attachment_height = 3

unit_count_y = 5
unit_count_x = 2
unit_length = mbk_1u.bounding_box().size.Y + sprue_width * 2
sprue_length = unit_length * (unit_count_y - 1) + attachment_length

with BuildPart() as sprue:
    with BuildSketch() as sprue_main_sk:
        Rectangle(sprue_width, sprue_length)
    extrude(amount=sprue_height)
    with BuildSketch(sprue.faces().sort_by(Axis.Z).last) as attachment_sk:
        with GridLocations(0, unit_length, 1, unit_count_y) as attachment_locs:
            Rectangle(attachment_width, attachment_length)
            attachment_locations = attachment_locs.locations
    attachments = extrude(amount=-attachment_height, clean=False)

    attachment_edges_to_fillet = (
        attachments.edges().group_by(Axis.Z)[-1].group_by(Axis.X)[0]
        + attachments.edges().group_by(Axis.Z)[-1].group_by(Axis.X)[-1]
    )

    fillet(attachment_edges_to_fillet, 0.5)

    for idx, loc in enumerate(attachment_locations):
        RigidJoint(
            f"attachment{idx * 2}",
            sprue.part,
            loc * Pos(attachment_width / 2, 0, -attachment_height),
        )
        RigidJoint(
            f"attachment{idx * 2 + 1}",
            sprue.part,
            loc * Pos(-attachment_width / 2, 0, -attachment_height) * Rot(0, 0, 180),
        )

mbk_1u.label = "Keycap"
sprue.part.label = "Sprue"
sprue.part.color = "grey"

# Create keycap copies and attach to joints
keycaps: list[Part] = []
for idx, attachment_keycap_joint in enumerate(sprue.part.joints.values()):
    keycap_copy = copy.copy(mbk_1u)
    attachment_keycap_joint.connect_to(keycap_copy.joints["edge"])
    keycap_copy.label += f" {idx}"
    keycaps.append(keycap_copy)

keycap_panel = Compound(
    label = "Keycap panel",
    children=[
        sprue.part,
        *keycaps,
    ]
)

keycap_panel.export_step("MBK_Keycap_1U_x10.step")
keycap_panel.export_stl("MBK_Keycap_1U_x10.stl")
show(
    keycap_panel,
    render_joints=False,
)