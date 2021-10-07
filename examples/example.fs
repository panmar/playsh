// Original example from https://www.shadertoy.com/view/WdsGRl
// Original author: naxius (https://www.shadertoy.com/user/naxius)

#version 330

in vec2 TEXCOORD;

uniform vec3 iResolution;
uniform float iTime;
uniform vec4 iMouse;
uniform sampler2D iChannel0;
uniform sampler2D iChannel1;

out vec4 fragColor;

void main() {
    vec2 uv = (TEXCOORD - .5 * iResolution.xy) / iResolution.y;
    float factor = mix(texture(iChannel0, uv).r, texture(iChannel1, uv).r, abs(sin(iTime)));
    float a = atan(uv.y, uv.x) * factor;
    float r = (0.5 + (iMouse.x / iResolution.x)) * length(uv);
    float counter = 100.;
    a = 4. * a + 20. * r + 50. * cos(r) * cos(.1 * iTime) + abs(a * r);
    float f = 0.02 * abs(cos(a)) / (r * r);

    vec2 v = vec2(0.);
    for(float i = 0.; i < counter; i++) {
        v = mat2(v, -v.y, v.x) * v + vec2(2. * f + cos(0.5 * iTime * (exp(-0.2 * r))), -cos(iTime * r * r) * cos(0.5 * iTime));
        if(length(v) > 2.) {
            counter = i;
            break;
        }
    }

    fragColor = min(0.9, 1.2 * exp(-pow(f, 0.45) * counter)) * (0.7 + 0.3 * cos(10. * r - 2. * iTime - vec4(.7, 1.4, 2.1, 0)));
}