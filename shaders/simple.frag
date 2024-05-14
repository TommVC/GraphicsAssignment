#version 330 core

uniform vec3 objectColor;
uniform vec4 ambprod; 
uniform vec4 diffprod; 
uniform vec4 specprod; 
float shine = 1;
in vec3 N; in vec3 L; in vec3 E;
in vec2 fragmentTexCoord;

out vec4 outColor;

uniform sampler2D imageTexture;

void main()
{
    vec3 NN = normalize(N);
    vec3 EE = normalize(E);
    vec3 LL = normalize(L);
    vec4 amb, diff, spec;
    vec3 H = normalize(LL+EE);
    float kd = max(dot(L,N), 0.0);
    float ks = pow(max(dot(N,H),0.0), shine);
    amb = ambprod;
    diff = kd*diffprod;
    spec = ks*specprod;
    outColor = (amb+diff+spec) * texture(imageTexture, fragmentTexCoord);
}
