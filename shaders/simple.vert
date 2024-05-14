#version 330 core

layout (location=0) in vec3 position;
layout (location=1) in vec2 vertexTexCoord;
layout (location=2) in vec3 norm;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;
uniform mat4 normMx;
uniform vec4 lposition;

out vec2 fragmentTexCoord;
out vec3 N; out vec3 L; out vec3 E;

void main()
{
    vec4 pos = model*vec4(position, 1.0f);
    N = (normMx*vec4(norm,1.0f)).xyz;
    L = (lposition).xyz + (-pos.xyz);
    E = -pos.xyz;
    gl_Position = projection * view * model * vec4(position, 1.0f);
    fragmentTexCoord = vertexTexCoord;
}
