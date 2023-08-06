#ifndef FIX64MATRIX3x3_H
#define FIX64MATRIX3x3_H

#include "Fix64Quaternion.h"

struct Fix64Matrix3x3
{
	Fix64Vector3 m_row[3];

	Fix64Matrix3x3() {}
	Fix64Matrix3x3(const Fix64Quaternion& quat)
	{
		this->setRotation(quat);
	}

	Fix64Matrix3x3(const Fix64Vector3& row0, const Fix64Vector3& row1, const Fix64Vector3& row2)
	{
		m_row[0] = row0;
		m_row[1] = row1;
		m_row[2] = row2;
	}
	

	Fix64Matrix3x3(const Fix64Scalar& xx, const Fix64Scalar& xy, const Fix64Scalar& xz, 
		const Fix64Scalar& yx, const Fix64Scalar& yy, const Fix64Scalar& yz, 
		const Fix64Scalar& zx, const Fix64Scalar& zy, const Fix64Scalar& zz)
	{
		setValue(xx, xy, xz, 
			yx, yy, yz, 
			zx, zy, zz);
	}

	

	void setValue(const Fix64Scalar& xx, const Fix64Scalar& xy, const Fix64Scalar& xz, 
		const Fix64Scalar& yx, const Fix64Scalar& yy, const Fix64Scalar& yz, 
		const Fix64Scalar& zx, const Fix64Scalar& zy, const Fix64Scalar& zz)
	{
		m_row[0].setValue(xx,xy,xz);
		m_row[1].setValue(yx,yy,yz);
		m_row[2].setValue(zx,zy,zz);
	}

	void setRotation(const Fix64Quaternion& q) 
	{
		Fix64Scalar d = q.length2();
		b3FullAssert(d != b3Scalar(0.0));
		Fix64Scalar s = Fix64Scalar::two() / d;
        
		Fix64Scalar xs = q.getX() * s,   ys = q.getY() * s,   zs = q.getZ() * s;
		Fix64Scalar wx = q.getW() * xs,  wy = q.getW() * ys,  wz = q.getW() * zs;
		Fix64Scalar xx = q.getX() * xs,  xy = q.getX() * ys,  xz = q.getX() * zs;
		Fix64Scalar yy = q.getY() * ys,  yz = q.getY() * zs,  zz = q.getZ() * zs;
		
		setValue(
            Fix64Scalar::one() - (yy + zz), xy - wz, xz + wy,
			xy + wz, Fix64Scalar::one() - (xx + zz), yz - wx,
			xz - wy, yz + wx, Fix64Scalar::one() - (xx + yy));
    }

	static Fix64Matrix3x3 getIdentity()
	{
		Fix64Matrix3x3 res(	Fix64Scalar::one(),Fix64Scalar::zero(),Fix64Scalar::zero(),
						Fix64Scalar::zero(),Fix64Scalar::one(),Fix64Scalar::zero(),
						Fix64Scalar::zero(),Fix64Scalar::zero(),Fix64Scalar::one());
		return res;
	}

	static Fix64Matrix3x3 zero()
	{
		Fix64Matrix3x3 res(	Fix64Scalar::zero(),Fix64Scalar::zero(),Fix64Scalar::zero(),
						Fix64Scalar::zero(),Fix64Scalar::zero(),Fix64Scalar::zero(),
						Fix64Scalar::zero(),Fix64Scalar::zero(),Fix64Scalar::zero());
		return res;
	}
	

	Fix64Matrix3x3 scaled(const Fix64Vector3& s) const
	{
		Fix64Matrix3x3 mat(
            m_row[0].getX() * s.getX(), m_row[0].getY() * s.getY(), m_row[0].getZ() * s.getZ(),
			m_row[1].getX() * s.getX(), m_row[1].getY() * s.getY(), m_row[1].getZ() * s.getZ(),
			m_row[2].getX() * s.getX(), m_row[2].getY() * s.getY(), m_row[2].getZ() * s.getZ());
		return mat;
	}

	static Fix64Matrix3x3 scale(const Fix64Vector3& s)
	{
		Fix64Matrix3x3 mat(
			Fix64Vector3::create(s.getX(), Fix64Scalar::zero(), Fix64Scalar::zero()),
			Fix64Vector3::create(Fix64Scalar::zero(), s.getY(), Fix64Scalar::zero()),
			Fix64Vector3::create(Fix64Scalar::zero(), Fix64Scalar::zero(), s.getZ()));
		return mat;
	}


	
	B3_FORCE_INLINE Fix64Matrix3x3 transposed() const 
	{
		return Fix64Matrix3x3( m_row[0].getX(), m_row[1].getX(), m_row[2].getX(),
							m_row[0].getY(), m_row[1].getY(), m_row[2].getY(),
							m_row[0].getZ(), m_row[1].getZ(), m_row[2].getZ());
	}

	

	

	B3_FORCE_INLINE Fix64Scalar tdotx(const Fix64Vector3& v) const 
	{
		return m_row[0].getX() * v.getX() + m_row[1].getX() * v.getY() + m_row[2].getX() * v.getZ();
	}
	B3_FORCE_INLINE Fix64Scalar tdoty(const Fix64Vector3& v) const 
	{
		return m_row[0].getY() * v.getX() + m_row[1].getY() * v.getY() + m_row[2].getY() * v.getZ();
	}
	B3_FORCE_INLINE Fix64Scalar tdotz(const Fix64Vector3& v) const 
	{
		return m_row[0].getZ() * v.getX() + m_row[1].getZ() * v.getY() + m_row[2].getZ() * v.getZ();
	}

	Fix64Vector3 transposeTimes(const Fix64Vector3& v)  const
	{
		//return Fix64Vector3::create(m[0].dot(v), m[1].dot(v), m[2].dot(v));
		return Fix64Vector3::create(tdotx(v), tdoty(v), tdotz(v));
	}


	B3_FORCE_INLINE const Fix64Vector3&  operator[](int i) const
	{ 
		//b3FullAssert(0 <= i && i < 3);
		return m_row[i]; 
	}

	Fix64Vector3 getCol0() const
	{
		Fix64Vector3 res = Fix64Vector3::create(m_row[0].getX(),m_row[1].getX(),m_row[2].getX());
		return res;
	}

	void setCol0(const Fix64Vector3& col)
	{
		m_row[0].m_x = col.m_x;
		m_row[1].m_x = col.m_y;
		m_row[2].m_x = col.m_z;
	}
	
	
	Fix64Vector3 getCol1() const
	{
		Fix64Vector3 res = Fix64Vector3::create(m_row[0].getY(),m_row[1].getY(),m_row[2].getY());
		return res;
	}

	void setCol1(const Fix64Vector3& col)
	{
		m_row[0].m_y = col.m_x;
		m_row[1].m_y = col.m_y;
		m_row[2].m_y = col.m_z;
	}

	Fix64Vector3 getCol2() const
	{
		Fix64Vector3 res = Fix64Vector3::create(m_row[0].getZ(),m_row[1].getZ(),m_row[2].getZ());
		return res;
	}

	void setCol2(const Fix64Vector3& col)
	{
		m_row[0].m_z = col.m_x;
		m_row[1].m_z = col.m_y;
		m_row[2].m_z = col.m_z;
	}

};

inline const Fix64Matrix3x3 transpose( const Fix64Matrix3x3 & mat )
{
	return mat.transposed();
}



inline const Fix64Matrix3x3 crossMatrix(const Fix64Vector3 & vec)
{
	//return Fix64Matrix3x3(
	//	Fix64Vector3::create(Fix64Scalar::zero(), vec.getZ(), -vec.getY()),
	//	Fix64Vector3::create(-vec.getZ(), Fix64Scalar::zero(), vec.getX()),
	//	Fix64Vector3::create(vec.getY(), -vec.getX(), Fix64Scalar::zero())
	//);

	return Fix64Matrix3x3(
		Fix64Vector3::create(Fix64Scalar::zero(), -vec.getZ(), vec.getY()),
		Fix64Vector3::create(vec.getZ(), Fix64Scalar::zero(), -vec.getX()),
		Fix64Vector3::create(-vec.getY(), vec.getX(), Fix64Scalar::zero())
	);

}


B3_FORCE_INLINE Fix64Vector3 
operator*(const Fix64Matrix3x3& m, const Fix64Vector3& v) 
{
	return Fix64Vector3::create(m[0].dot(v), m[1].dot(v), m[2].dot(v));

}


B3_FORCE_INLINE Fix64Matrix3x3 operator-(const Fix64Matrix3x3& m1, const Fix64Matrix3x3& m2)
{
	return Fix64Matrix3x3(m1.m_row[0] - m2.m_row[0], m1.m_row[1] - m2.m_row[1], m1.m_row[2] - m2.m_row[2] );
}


B3_FORCE_INLINE Fix64Matrix3x3 operator*(const Fix64Matrix3x3& m1, const Fix64Matrix3x3& m2)
{
	return Fix64Matrix3x3(
		m2.tdotx( m1[0]), m2.tdoty( m1[0]), m2.tdotz( m1[0]),
		m2.tdotx( m1[1]), m2.tdoty( m1[1]), m2.tdotz( m1[1]),
		m2.tdotx( m1[2]), m2.tdoty( m1[2]), m2.tdotz( m1[2]));
}

#endif

