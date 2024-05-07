#version 330 core

uniform vec3 objectColor;
in vec2 fragmentTexCoord;

out vec4 outColor;

uniform sampler2D imageTexture;

void main()
{
    outColor = vec4(objectColor,1) * texture(imageTexture, fragmentTexCoord);
}
